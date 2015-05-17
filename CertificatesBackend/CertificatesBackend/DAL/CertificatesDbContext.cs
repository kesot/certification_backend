using System;
using System.Data.Entity;
using System.Linq;
using CertificatesBackend.Models;

namespace CertificatesBackend.DAL
{
	internal interface IEntityWithId
	{
		int Id { get; set; }
	}
	internal static class DbSetExtensions
	{
		public static T TryGetById<T>(this DbSet<T> dbSet, int id) where T : class, IEntityWithId
		{
			return dbSet.SingleOrDefault(e => e.Id == id);
		}
	}
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