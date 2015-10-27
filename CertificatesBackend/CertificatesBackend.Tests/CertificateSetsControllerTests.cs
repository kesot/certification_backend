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
	public class CertificateSetsControllerTests: TestBase
	{
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
			var acquiredCertificateSets = controller.GetCertificateSets(0, 10);
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
			
			Assert.AreEqual("24400222284", DbContext.Certificates.First(c => c.CertificateSetId == 1).CodeValue);
			Assert.AreEqual(100, DbContext.Certificates.Count(c => c.CertificateSetId == 1));

		}
	}
}
