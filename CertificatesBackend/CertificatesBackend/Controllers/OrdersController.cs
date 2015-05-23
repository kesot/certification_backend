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
	public class OrdersController : BaseController
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
			return db.Orders.Where(o => o.UserExternalId == userId).Include(o => o.Certificates.Select(c => c.CertificateSet));
		}

		[Route("api/Orders/last-unpaid/{userid}")]
		[ResponseType(typeof(Order))]
		public Order GetLastUnpayed(int userId)
		{
			return db.Orders.Where(o => o.UserExternalId == userId && o.PaymentDateTimeUtc == null )
				.Include(o => o.Certificates.Select(c => c.CertificateSet)).SingleOrDefault();
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
		/// Добавление в заказ сертификатов. Выполняется атомарно (либо все, либо ни один)
		/// </summary>
		/// <param name="id">id заказа</param>
		/// <param name="certificateIds">JSON массив id сертификатов, которые добавляем в заказ</param>
		/// <returns></returns>
		[HttpPost]
		[Route("api/Orders/{id}/add-certificates")]
		[ResponseType(typeof (ResponseMessageResult))]
		public IHttpActionResult AddCertificate(int id, int[] certificateIds)
		{
			var order = db.Orders.TryGetById(id);
			if (order == null)
				return BadRequest(string.Format("Order #{0} not found", id));

			foreach (var certificateId in certificateIds)
			{
				var certificate = db.Certificates.TryGetById(certificateId);
				if (certificate == null)
					return BadRequest(string.Format("Certificate #{0} not found", id));
				db.Entry(certificate).State = EntityState.Modified;
				certificate.OrderId = id;
			}
			
			db.SaveChanges();

			return ResponseMessage(new HttpResponseMessage(HttpStatusCode.Accepted));
		}


		[HttpDelete]
		[Route("api/Orders/{id}/remove-certificates")]
		[ResponseType(typeof(ResponseMessageResult))]
		public IHttpActionResult RemoveCertificates(int id, int[] certificateIds)
		{
			var order = db.Orders.TryGetById(id);
			if (order == null)
				return BadRequest(string.Format("Order #{0} not found", id));
			if (order.PaymentDateTimeUtc != null)
				return BadRequest(string.Format("Order #{0} already payed", id));

			foreach (var certificateId in certificateIds)
			{
				var certificate = db.Certificates.TryGetById(certificateId);
				if (certificate == null)
					return BadRequest(string.Format("Certificate #{0} not found", id));
				if (certificate.OrderId != order.Id)
					return BadRequest(string.Format("Certificate #{0} dont belong to order #{1}", id, order.Id));
				db.Entry(certificate).State = EntityState.Modified;
				certificate.OrderId = null;
			}

			db.SaveChanges();

			return ResponseMessage(new HttpResponseMessage(HttpStatusCode.Accepted));
		}

		/// <summary>
		/// Пометить заказ как оплаченный
		/// </summary>
		/// <param name="id">id заказа</param>
		/// <returns>Сертификаты входившие в заказ</returns>
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
		/// Отменить заказ. Невозможно отменить оплаченный заказ.
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