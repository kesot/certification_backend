using System.Data.Entity;
using CertificatesBackend.Models;

namespace CertificatesBackend.DAL
{
	public class CertificatesDbContext: DbContext
	{
		public CertificatesDbContext()
			: base("CertificatesDbContext")
		{
		}

		public virtual DbSet<Certificate> Certificates { get; set; }
		public virtual DbSet<CertificateSet> CertificateSets { get; set; }
		public virtual DbSet<Company> Companies { get; set; }
		public virtual DbSet<Order> Orders { get; set; }
	}
}