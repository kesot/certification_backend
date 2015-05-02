using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.Http.Description;
using CertificatesBackend.DAL;
using CertificatesBackend.Models;

namespace CertificatesBackend.Controllers
{
	public class CertificatesController : ApiController
	{
		private CertificatesDbContext db = new CertificatesDbContext();

		// GET api/Certificate
		public IQueryable<Certificate> GetCertificates()
		{
			return db.Certificates;
		}

		// GET api/Certificate/5
		[ResponseType(typeof(Certificate))]
		public async Task<IHttpActionResult> GetCertificate(int id)
		{
			Certificate certificate = await db.Certificates.FindAsync(id);
			if (certificate == null)
			{
				return NotFound();
			}

			return Ok(certificate);
		}

		protected override void Dispose(bool disposing)
		{
			if (disposing)
			{
				db.Dispose();
			}
			base.Dispose(disposing);
		}

		private bool CertificateExists(int id)
		{
			return db.Certificates.Count(e => e.Id == id) > 0;
		}
	}
}