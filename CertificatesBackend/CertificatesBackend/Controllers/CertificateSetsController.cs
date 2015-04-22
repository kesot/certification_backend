using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.Http.Description;
using System.Web.Http.Results;
using CertificatesBackend.DAL;
using CertificatesBackend.Models;

namespace CertificatesBackend.Controllers
{
	public class CertificateSetsController : ApiController
	{
		private CertificatesDbContext db = new CertificatesDbContext();

		public CertificateSetsController()
		{
		}

		public CertificateSetsController(CertificatesDbContext context)
		{
			db = context;
		}
		// GET api/CertificateSets
		public IHttpActionResult GetCertificateSets()
		{
			return Ok(db.CertificateSets.AsEnumerable());
		}

		// GET api/CertificateSets/5
		[ResponseType(typeof(CertificateSet))]
		public IHttpActionResult GetCertificateSet(int id)
		{
			CertificateSet certificateset = db.CertificateSets.Find(id);
			if (certificateset == null)
			{
				return NotFound();
			}

			return Ok(certificateset);
		}

		// PUT api/CertificateSets/5
		public IHttpActionResult PutCertificateSet(int id, CertificateSet certificateset)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			if (id != certificateset.Id)
			{
				return BadRequest();
			}

			db.Entry(certificateset).State = EntityState.Modified;

			try
			{
				db.SaveChanges();
			}
			catch (DbUpdateConcurrencyException)
			{
				if (!CertificateSetExists(id))
				{
					return NotFound();
				}
				else
				{
					throw;
				}
			}

			return StatusCode(HttpStatusCode.NoContent);
		}

		/// <summary>
		/// Добавление шаблона (набора) сертификатов
		/// </summary>
		/// <param name="certificateset">Модель набора сертификатов</param>
		/// <remarks>Insert new student</remarks>
		/// <response code="400">Bad request</response>
		/// <response code="500">Internal Server Error</response>
		// POST api/CertificateSets
		[Route("api/CertificateSets/Add")]
		[HttpPost]
		[ResponseType(typeof(ResponseMessageResult))]
		public IHttpActionResult PostCertificateSet(CertificateSet certificateset)
		{
			if (certificateset == null)
				return BadRequest("CertificateSet is null");
			if (!ModelState.IsValid)
				return BadRequest(ModelState);

			db.CertificateSets.Add(certificateset);
			db.SaveChanges();
			return ResponseMessage(new HttpResponseMessage(HttpStatusCode.Created));
		}
		[Route("api/CertificateSets/{id:int}/GenerateCertificates")]
		[HttpPost]
		[ResponseType(typeof(CertificateSet))]
		public IHttpActionResult GenereteCertificates(int id)
		{
			var certificateSet = db.CertificateSets.Find(id);
			if (certificateSet == null)
				return BadRequest(string.Format("Certificate #{0} not found", id));
			
			Task.Run(() =>
			{
				Thread.Sleep(100000);
				var a = 1;
			});
			return ResponseMessage(new HttpResponseMessage(HttpStatusCode.Accepted));
		}

		// DELETE api/CertificateSets/5
		[ResponseType(typeof(CertificateSet))]
		public IHttpActionResult DeleteCertificateSet(int id)
		{
			CertificateSet certificateset = db.CertificateSets.Find(id);
			if (certificateset == null)
			{
				return NotFound();
			}

			db.CertificateSets.Remove(certificateset);
			db.SaveChanges();

			return Ok(certificateset);
		}

		protected override void Dispose(bool disposing)
		{
			if (disposing)
			{
				db.Dispose();
			}
			base.Dispose(disposing);
		}

		private bool CertificateSetExists(int id)
		{
			return db.CertificateSets.Count(e => e.Id == id) > 0;
		}
	}
}