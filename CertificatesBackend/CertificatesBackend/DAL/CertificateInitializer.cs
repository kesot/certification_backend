using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using CertificatesBackend.Models;

namespace CertificatesBackend.DAL
{
	public class CertificateInitializer : System.Data.Entity.DropCreateDatabaseIfModelChanges<CertificatesDbContext>
	{
		protected override void Seed(CertificatesDbContext context)
		{
			context.Companies.Add(new Company
			{
				Name = "MVideo"
			});
			context.SaveChanges();
			
			context.CertificateSets.Add(new CertificateSet
			{
				CompanyId = 1,
				Descitption = "CertificateSet descr",
				MaskString = "244???2384",
				Name = "Подарочный сертификат на 1000 р",
				AdministrativeName = "1000 Рублевые сертификаты со скидкой",
				CostValue = 1000,
				Price = 900
			});
			context.SaveChanges();

			context.Certificates.Add(new Certificate
			{
				CertificateSetId = 1,
				CodeValue = "2440012384"
			});
			context.SaveChanges();
		}
	}
}