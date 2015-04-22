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
	public class UnitTest1
	{
		private Mock<CertificatesDbContext> MockContext;

		[TestInitialize]
		public void TestInitialize()
		{
			var companies = new List<Company>
			{
				new Company()
				{
					Id = 1,
					Name = "Company1"
				}
			};
			var certificateSets = new List<CertificateSet>
			{
				new CertificateSet
				{
					Id = 1,
					CompanyId = 1,
					Descitption = "CertificateSet descr",
					MaskString = "244???222284",
					Name = "Подарочный сертификат на 1000 р",
					AdministrativeName = "1000 Рублевые сертификаты со скидкой",
					CostValue = 1000,
					Price = 900
				},
				new CertificateSet
				{
					Id = 2,
					CompanyId = 1,
					Descitption = "CertificateSet descr2",
					MaskString = "244???2384",
					Name = "Подарочный сертификат на 1000 р",
					AdministrativeName = "1000 Рублевые сертификаты со скидкой",
					CostValue = 1000,
					Price = 900
				},
			}.AsQueryable();

			var mockSet = new Mock<DbSet<CertificateSet>>();
			mockSet.As<IQueryable<CertificateSet>>().Setup(m => m.Provider).Returns(certificateSets.Provider);
			mockSet.As<IQueryable<CertificateSet>>().Setup(m => m.Expression).Returns(certificateSets.Expression);
			mockSet.As<IQueryable<CertificateSet>>().Setup(m => m.ElementType).Returns(certificateSets.ElementType);
			mockSet.As<IQueryable<CertificateSet>>().Setup(m => m.GetEnumerator()).Returns(certificateSets.GetEnumerator());

			MockContext = new Mock<CertificatesDbContext>();
			MockContext.Setup(c => c.CertificateSets).Returns(mockSet.Object);
		}
		[TestMethod]
		public void TestMethod1()
		{

			var controller = new TestController
			{
				Request = new HttpRequestMessage(),
				Configuration = new HttpConfiguration()
			};

			// Act
			var response = ((OkNegotiatedContentResult<string[]>)controller.Get()).Content;

			Assert.AreEqual("value1", response[0]);
			// Assert
		}
		[TestMethod]
		public void GetCertificateSets()
		{
			var controller = new CertificateSetsController(MockContext.Object)
			{
				Request = new HttpRequestMessage(),
				Configuration = new HttpConfiguration()
			};
			var acquiredCertificateSets = controller.GetCertificateSets();
			var response = ((OkNegotiatedContentResult<IEnumerable<CertificateSet>>)acquiredCertificateSets).Content.ToList();
			Assert.AreEqual(2, response.Count);
			Assert.AreEqual("244???222284", response[0].MaskString);
			Assert.AreEqual("Подарочный сертификат на 1000 р", response[0].Name);
		}
	}
}
