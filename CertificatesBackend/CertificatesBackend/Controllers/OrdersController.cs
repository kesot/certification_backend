using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Description;
using System.Web.Http.Results;
using CertificatesBackend.Models;
using CertificatesBackend.DAL;

namespace CertificatesBackend.Controllers
{
	/// <summary>
	/// Работа с заказами.
	/// </summary>
	public class OrdersController : ApiController
	{
		private readonly CertificatesDbContext db = new CertificatesDbContext();

		public OrdersController()
		{
		}

		public OrdersController(CertificatesDbContext context)
		{
			db = context;
		}

		/// <summary>
		/// Получение списка заказов пользователя.
		/// </summary>
		/// <param name="userId">Внешний id пользователя.</param>
		/// <returns>Список заказов</returns>
		[Route("api/Orders/ByUser/{userid}")]
		[ResponseType(typeof(Order[]))]
		public IQueryable<Order> GetOrders(int userId)
		{
			return db.Orders.Where(o => o.UserExternalId == userId).Include(o => o.Certificates);
		}

		/// <summary>
		/// Получение заказа по id.
		/// </summary>
		/// <param name="id"></param>
		/// <returns></returns>
		[HttpGet]
		[ResponseType(typeof(Order))]
		[Route("api/Orders/{id}", Name = "GetOrder")]
		public IHttpActionResult GetOrder(int id)
		{
			Order order = db.Orders.TryGetById(id);
			if (order == null)
			{
				return NotFound();
			}

			return Ok(order);
		}

		/// <summary>
		/// Создание заказа для пользователя
		/// </summary>
		/// <param name="userId"></param>
		/// <returns></returns>
		[HttpPost]
		[Route("api/Orders/create-for-user/{userId}")]
		[ResponseType(typeof(Order))]
		public IHttpActionResult CreateForUser(int userId)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			var order = new Order()
			{
				UserExternalId = userId
			};

			db.Orders.Add(order);
			db.SaveChanges();

			return CreatedAtRoute("GetOrder", new {order.Id}, order);
		}

		/// <summary>
		/// Пометить заказ как оплаченный
		/// </summary>
		/// <param name="id"></param>
		/// <returns></returns>
		[HttpPost]
		[Route("api/Orders/{id}/confirm-payment")]
		[ResponseType(typeof (Certificate[]))]
		public IHttpActionResult ConfirmPayment(int id)
		{
			var order = db.Orders.TryGetById(id);
			if (order == null)
				return BadRequest(string.Format("Order #{0} not found",id));
			if (order.PaymentDateTimeUtc != null)
				return BadRequest(string.Format("Order #{0} already payed", id));

			order.PaymentDateTimeUtc = DateTime.UtcNow;
			db.Entry(order).State = EntityState.Modified;

			db.SaveChanges();

			return Ok(db.Certificates.Where(c => c.OrderId == order.Id));
		}

		/// <summary>
		/// Отменить заказ
		/// </summary>
		/// <param name="id"></param>
		/// <returns></returns>
		[HttpPost]
		[Route("api/Orders/{id}/Cancel")]
		[ResponseType(typeof(ResponseMessageResult))]
		public IHttpActionResult Cancel(int id)
		{
			var order = db.Orders.TryGetById(id);
			if (order == null)
				return BadRequest(string.Format("Order #{0} not found", id));
			if (order.PaymentDateTimeUtc != null)
				return BadRequest(string.Format("Order #{0} already payed", id));
			if (order.IsCanceled)
				return BadRequest(string.Format("Order #{0} already canceled", id));

			order.IsCanceled = true;
			foreach (var certificate in db.Certificates.Where(c => c.OrderId == id))
			{
				certificate.OrderId = null;
				db.Entry(certificate).State = EntityState.Modified;
			}

			db.Entry(order).State = EntityState.Modified;

			db.SaveChanges();

			return ResponseMessage(new HttpResponseMessage(HttpStatusCode.Accepted));
		}

		protected override void Dispose(bool disposing)
		{
			if (disposing)
			{
				db.Dispose();
			}
			base.Dispose(disposing);
		}

		private bool OrderExists(int id)
		{
			return db.Orders.Count(e => e.Id == id) > 0;
		}
	}
}