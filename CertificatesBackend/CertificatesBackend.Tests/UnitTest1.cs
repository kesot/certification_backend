using System;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Results;
using System.Web.Script.Serialization;
using CertificatesBackend.Controllers;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace CertificatesBackend.Tests
{
    [TestClass]
    public class UnitTest1
    {
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
    }
}
