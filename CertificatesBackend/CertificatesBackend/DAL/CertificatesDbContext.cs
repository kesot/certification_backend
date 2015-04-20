using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Data.Entity.ModelConfiguration.Conventions;
using System.Linq;
using System.Web;
using CertificatesBackend.Models;

namespace CertificatesBackend.DAL
{
	public class CertificatesDbContext: DbContext
	{
		public CertificatesDbContext()
			: base("CertificatesDbContext")
		{
		}

		public DbSet<Certificate> Certificates { get; set; }
		public DbSet<CertificateSet> CertificateSets { get; set; }
		public DbSet<Company> Companies { get; set; }
		public DbSet<Order> Orders { get; set; }
	}
}