using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace CertificatesBackend.Models
{
	public class CertificateSet
	{
		public int Id { get; set; }
		public string MaskString { get; set; }
		public string AdministrativeName { get; set; }
		public string Name { get; set; }
		public string Descitption { get; set; }
		public int CompanyId { get; set; }

		// Цена для покупателя
		public int Price { get; set; }
		// Номинал сертификата
		public int CostValue { get; set; }

		public virtual Company Company { get; set; }
	}
}