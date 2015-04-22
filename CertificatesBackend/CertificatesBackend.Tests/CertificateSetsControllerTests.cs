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
	public static class Mocker
	{
		public static Mock<DbSet<T>> GetMockDbSetFor<T>(List<T> entitiesList) where T : class
		{
			var queriableList = entitiesList.AsQueryable();
			var mockDbSet = new Mock<DbSet<T>>();
			mockDbSet.As<IQueryable<T>>().Setup(m => m.Provider).Returns(queriableList.Provider);
			mockDbSet.As<IQueryable<T>>().Setup(m => m.Expression).Returns(queriableList.Expression);
			mockDbSet.As<IQueryable<T>>().Setup(m => m.ElementType).Returns(queriableList.ElementType);
			mockDbSet.As<IQueryable<T>>().Setup(m => m.GetEnumerator()).Returns(entitiesList.GetEnumerator());
			mockDbSet.Setup(m => m.Add(It.IsAny<T>())).Callback((T t) =>
			{
				entitiesList.Add(t);
			});

			return mockDbSet;
		}
	}
	[TestClass]
	public class CertificateSetsControllerTests
	{
		protected Mock<CertificatesDbContext> MockContext;
		protected CertificatesDbContext DbContext;
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
					MaskString = "244??222284",
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
			};

			var certificates = new List<Certificate>()
				;

			var mockCertificateSets = Mocker.GetMockDbSetFor(certificateSets);
			var mockCertificates = Mocker.GetMockDbSetFor(certificates);

			MockContext = new Mock<CertificatesDbContext>();
			MockContext.Setup(c => c.CertificateSets).Returns(mockCertificateSets.Object);
			MockContext.Setup(c => c.Certificates).Returns(mockCertificates.Object);
			DbContext = MockContext.Object;
		}

		private CertificateSetsController GetController()
		{
			return new CertificateSetsController(MockContext.Object)
			{
				Request = new HttpRequestMessage(),
				Configuration = new HttpConfiguration()
			};
		}
		[TestMethod]
		public void GetCertificateSets()
		{
			var controller = GetController();
			var acquiredCertificateSets = controller.GetCertificateSets();
			var response = ((OkNegotiatedContentResult<IEnumerable<CertificateSet>>)acquiredCertificateSets).Content.ToList();
			Assert.AreEqual(2, response.Count);
			Assert.AreEqual("244??222284", response[0].MaskString);
			Assert.AreEqual("Подарочный сертификат на 1000 р", response[0].Name);
		}

		[TestMethod]
		public void GenerateCertificates()
		{
			var controller = GetController();
			var response = controller.GenereteCertificates(1) as ResponseMessageResult;
			Assert.IsTrue(response.Response.IsSuccessStatusCode);
			Assert.IsTrue(DbContext.CertificateSets.SingleOrDefault(c => c.Id == 1).IsInCertificateGeneratingStage);
			while (DbContext.CertificateSets.SingleOrDefault(c => c.Id == 1).IsInCertificateGeneratingStage);
			
			Assert.AreEqual("24400222284", DbContext.Certificates.First().CodeValue);
			Assert.AreEqual(100, DbContext.Certificates.Count());

		}
	}
}
