using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Results;
using CertificatesBackend.DAL;
using CertificatesBackend.Models;

namespace CertificatesBackend.Controllers
{
	public class TestController : ApiController
	{
		public IHttpActionResult Get()
		{
			var context = new CertificatesDbContext();

			return Ok(context.Certificates.First());
		}
	}
}
