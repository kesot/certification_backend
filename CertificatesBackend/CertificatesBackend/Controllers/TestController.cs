using System.Linq;
using System.Web.Http;
using CertificatesBackend.DAL;

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
