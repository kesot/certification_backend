﻿using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Description;
using CertificatesBackend.Models;
using CertificatesBackend.DAL;

namespace CertificatesBackend.Controllers
{
	/// <summary>
	/// Работа с заказами.
	/// </summary>
	public class OrdersController : ApiController
	{
		private CertificatesDbContext db = new CertificatesDbContext();


		/// <summary>
		/// Получение списка заказов пользователя.
		/// </summary>
		/// <param name="userId">Внешний id пользователя.</param>
		/// <returns>Список заказов</returns>
		[Route("api/Orders/ByUser/{userid}")]
		[ResponseType(typeof(Order[]))]
		public IQueryable<Order> GetOrders(int userId)
		{
			return db.Orders.Where(o => o.UserExternalId == userId);
		}

		/// <summary>
		/// Получение заказа по id.
		/// </summary>
		/// <param name="id"></param>
		/// <returns></returns>
		[ResponseType(typeof(Order))]
		public IHttpActionResult GetOrder(int id)
		{
			Order order = db.Orders.Find(id);
			if (order == null)
			{
				return NotFound();
			}

			return Ok(order);
		}

		// POST api/Orders
		[ResponseType(typeof(Order))]
		public IHttpActionResult PostOrder(Order order)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			db.Orders.Add(order);
			db.SaveChanges();

			return CreatedAtRoute("DefaultApi", new { id = order.Id }, order);
		}

		// DELETE api/Orders/5
		[ResponseType(typeof(Order))]
		public IHttpActionResult DeleteOrder(int id)
		{
			Order order = db.Orders.Find(id);
			if (order == null)
			{
				return NotFound();
			}

			db.Orders.Remove(order);
			db.SaveChanges();

			return Ok(order);
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