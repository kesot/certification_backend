﻿using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using System.Web.Http.Description;
using CertificatesBackend.Models;
using CertificatesBackend.DAL;

namespace CertificatesBackend.Controllers
{
	public class CompaniesController : ApiController
	{
		private CertificatesDbContext db = new CertificatesDbContext();

		// GET api/Companies
		public IQueryable<Company> GetCompanies()
		{
			return db.Companies;
		}

		// GET api/Companies/5
		[ResponseType(typeof(Company))]
		public IHttpActionResult GetCompany(int id)
		{
			Company company = db.Companies.TryGetById(id);
			if (company == null)
			{
				return BadRequest("Not found such company");
			}

			return Ok(company);
		}

		// GET api/Companies/5
		[Route("api/Companies/ByName")]
		[ResponseType(typeof(Company))]
		public IHttpActionResult GetByName(string companyName)
		{
			Company company = db.Companies.SingleOrDefault(c => c.Name == companyName);
			if (company == null)
			{
				return BadRequest("Not found such company");
			}

			return Ok(company);
		}

		// PUT api/Companies/5
		public IHttpActionResult PutCompany(int id, Company company)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			if (id != company.Id)
			{
				return BadRequest();
			}

			db.Entry(company).State = EntityState.Modified;

			try
			{
				db.SaveChanges();
			}
			catch (DbUpdateConcurrencyException)
			{
				if (!CompanyExists(id))
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

		// POST api/Companies
		[ResponseType(typeof(Company))]
		public IHttpActionResult PostCompany(Company company)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			db.Companies.Add(company);
			db.SaveChanges();

			return CreatedAtRoute("DefaultApi", new { id = company.Id }, company);
		}

		// DELETE api/Companies/5
		[ResponseType(typeof(Company))]
		public IHttpActionResult DeleteCompany(int id)
		{
			Company company = db.Companies.Find(id);
			if (company == null)
			{
				return NotFound();
			}

			db.Companies.Remove(company);
			db.SaveChanges();

			return Ok(company);
		}

		protected override void Dispose(bool disposing)
		{
			if (disposing)
			{
				db.Dispose();
			}
			base.Dispose(disposing);
		}

		private bool CompanyExists(int id)
		{
			return db.Companies.Count(e => e.Id == id) > 0;
		}
	}
}