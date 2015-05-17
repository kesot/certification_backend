using System;
using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using System.Web.Http;
using System.Web.Http.Description;
using System.Web.Http.Results;
using CertificatesBackend.DAL;
using CertificatesBackend.Models;

namespace CertificatesBackend.Controllers
{
	/// <summary>
	/// Работа с наборами сертификатов
	/// </summary>
	public class CertificateSetsController : BaseController
	{
		private CertificatesDbContext db = new CertificatesDbContext();

		public CertificateSetsController()
		{
		}

		public CertificateSetsController(CertificatesDbContext context)
		{
			db = context;
		}
		
		
		/// <summary>
		/// Все наборы сертификатов в бд, c пэйджингом
		/// </summary>
		/// <param name="pageIndex">По умолчанию 0</param>
		/// <param name="pageSize">По умолчанию 10</param>
		/// <param name="onlyWithAvailable">Только с доступными для заказа сертификатами</param> 
		/// <returns></returns>
		[HttpGet]
		[Route("api/CertificateSets")]
		[ResponseType(typeof(CertificateSet[]))]
		public IHttpActionResult GetCertificateSets(int pageIndex = 0, int pageSize = 10, bool onlyWithAvailable = true)
		{
			return Ok(db.CertificateSets.Where(cs => db.Certificates.Where(c => c.CertificateSetId == cs.Id).Any(c => c.OrderId == null) || !onlyWithAvailable)
				.OrderBy(c => c.Id).Skip(pageIndex * pageSize)
				.Take(pageSize)
				.AsEnumerable());
		}


		/// <summary>
		/// Наборы кодов по компании
		/// </summary>
		/// <param name="companyId"></param>
		/// <param name="onlyWithAvailable">Только с доступными для заказа сертификатами</param> 
		/// <returns></returns>
		[Route("api/CertificateSets/ByCompany")]
		[ResponseType(typeof (CertificateSet[]))]
		[HttpGet]
		public IHttpActionResult GetCertificatesByCompany(int companyId, bool onlyWithAvailable = true)
		{
			return Ok(db.CertificateSets.Where(cs => db.Certificates.Where(c => c.CertificateSetId == cs.Id).Any(c => c.OrderId == null) || !onlyWithAvailable)
				.Where(c => c.CompanyId == companyId));
		}

		/// <summary>
		/// Получение первого доступного сертификата из набора. Если в наборе нет доступных - NotFound
		/// </summary>
		/// <param name="id"></param>
		/// <returns></returns>
		[Route("api/CertificateSets/{id}/first-available-certificate")]
		[ResponseType(typeof(Certificate))]
		[HttpGet]
		public IHttpActionResult GetFirstAvailable(int id)
		{
			var certificateSet = db.CertificateSets.TryGetById(id);
			if (certificateSet == null)
				return BadRequest(string.Format("CertificateSet #{0} not found", id));
			var certificate = db.Certificates.First(c => c.OrderId == null && c.CertificateSetId == id);
			if (certificate == null)
				return NotFound();
			return Ok(certificate);
		}

		// GET api/CertificateSets/5
		[ResponseType(typeof(CertificateSet))]
		public IHttpActionResult GetCertificateSet(int id)
		{
			CertificateSet certificateset = db.CertificateSets.TryGetById(id);
			if (certificateset == null)
			{
				return NotFound();
			}

			return Ok(certificateset);
		}

		
		/// <summary>
		/// Изменение набора сертификатов
		/// </summary>
		/// <param name="id"></param>
		/// <param name="сertificateSet"></param>
		/// <returns>Статус или сообщение об ошибке</returns>
		[ResponseType(typeof(StatusCodeResult))]
		public IHttpActionResult PutCertificateSet(int id, CertificateSet сertificateSet)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			if (id != сertificateSet.Id)
			{
				return BadRequest();
			}

			db.Entry(сertificateSet).State = EntityState.Modified;

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

		/// <summary>
		/// Запускает задачу генерации сертификатов в наборе
		/// </summary>
		/// <param name="id">id набора сертификатов</param>
		/// <returns></returns>
		[Route("api/CertificateSets/{id:int}/generate-certificates")]
		[HttpPost]
		[ResponseType(typeof(ResponseMessageResult))]
		public IHttpActionResult GenereteCertificates(int id)
		{
			var certificateSet = db.CertificateSets.SingleOrDefault(cs => cs.Id == id);
			if (certificateSet == null)
				return BadRequest(string.Format("CertificateSet #{0} not found", id));
			if (certificateSet.IsInCertificateGeneratingStage)
				return BadRequest(string.Format("CertificateSet #{0} already in generating state", id));
			if (certificateSet.AllCertificatesGenerated)
				return BadRequest(string.Format("CertificateSet #{0} already generated all certificates", id));

			certificateSet.GenerateCertificates(db);
			
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
			if (db.Certificates.Any(c => c.CertificateSetId == id))
				return BadRequest(string.Format("CertificateSet #{0} имеет связанные сертификаты", id));

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
			return db.CertificateSets.Any(c => c.Id == id);
		}
	}
}