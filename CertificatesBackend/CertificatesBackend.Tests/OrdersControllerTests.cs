using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Net.Http;
using System.Web.Http;
using System.Web.Script.Serialization;
using CertificatesBackend.Controllers;
using CertificatesBackend.DAL;
using CertificatesBackend.Models;
using System.Web.Http.Results;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;

namespace CertificatesBackend.Tests
{
	
	[TestClass]
	public class OrdersControllerTests: TestBase
	{
		private OrdersController controller;
		
		[TestInitialize]
		public override void TestInitialize()
		{
			base.TestInitialize();
			controller = new OrdersController(MockContext.Object)
			{
				Request = new HttpRequestMessage(),
				Configuration = new HttpConfiguration()
			};
		}

		[TestMethod]
		public void AddCertificate()
		{
			var response = controller.AddCertificate(1, new[] {1}) as ResponseMessageResult;
		}

		[TestMethod]
		public void ConfirmPayment()
		{
			var response = controller.ConfirmPayment(1);
		}
		
		[TestMethod]
		public void GetOrdersByUser()
		{
			var response = controller.GetOrders(2).ToList();

			Assert.AreEqual(2, response.Count);
			Assert.AreEqual(2, response[0].UserExternalId);
			Assert.IsTrue(response.Any(o => o.Id == 2) && response.Any(o => o.Id == 3));
		}

		[TestMethod]
		public void GetOrderById()
		{
			var response = controller.GetOrder(1) as OkNegotiatedContentResult<Order>;

			Assert.AreEqual(1, response.Content.Id);
			Assert.AreEqual(1, response.Content.UserExternalId);
		}

		[TestMethod]
		public void CreateForUser()
		{
			var response = controller.CreateForUser(101);
			var responseObject = ((CreatedAtRouteNegotiatedContentResult<Order>)response).Content;

			Assert.IsTrue(DbContext.Orders.Count(o => o.UserExternalId == 101) == 1);
		}

		[TestMethod]
		public void Cancel()
		{
			var response = controller.Cancel(1) as ResponseMessageResult;
			Assert.IsTrue(DbContext.Orders.Single(o => o.Id == 1).IsCanceled);
			Assert.AreEqual(null, DbContext.Certificates.Single(o => o.Id == 1).OrderId);
		}

		[TestMethod]
		public void CancelationError()
		{
			var response = controller.Cancel(2) as BadRequestErrorMessageResult;
			
			Assert.AreEqual(string.Format("Order #{0} already payed", 2), response.Message);
		}
	}
}
