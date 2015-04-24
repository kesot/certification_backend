using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CertificatesBackend.DAL;
using CertificatesBackend.Models;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Moq;

namespace CertificatesBackend.Tests
{
	public static class MockerExtensions
	{
		public static Mock<DbSet<T>> GetMockDbSet<T>(this List<T> entitiesList) where T: class
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
	public abstract class TestBase
	{
		protected Mock<CertificatesDbContext> MockContext;
		protected CertificatesDbContext DbContext;

		[TestInitialize]
		public virtual void TestInitialize()
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
			{
				new Certificate()
				{
					CertificateSetId = 2,
					CodeValue = "123123",
					Id = 1
				},
				new Certificate()
				{
					CertificateSetId = 2,
					CodeValue = "123123",
					Id = 2,
					OrderId = 1
				},
				new Certificate()
				{
					CertificateSetId = 2,
					CodeValue = "123123",
					Id = 2,
					OrderId = 2,
				}
			};

			var orders = new List<Order>()
			{
				new Order()
				{
					Id = 1,
					UserExternalId = 1,
				},
				new Order()
				{
					Id = 3,
					UserExternalId = 2,
				},
				new Order()
				{
					Id = 2,
					UserExternalId = 2,
					PaymentDateTimeUtc = new DateTime(2011,10,12)
				}
			};

			var mockCertificateSets = certificateSets.GetMockDbSet();
			var mockCertificates = certificates.GetMockDbSet();
			var mockOrders = orders.GetMockDbSet();

			MockContext = new Mock<CertificatesDbContext>();
			MockContext.Setup(c => c.CertificateSets).Returns(mockCertificateSets.Object);
			MockContext.Setup(c => c.Certificates).Returns(mockCertificates.Object);
			MockContext.Setup(c => c.Orders).Returns(mockOrders.Object);
			DbContext = MockContext.Object;
		}
	}
}
