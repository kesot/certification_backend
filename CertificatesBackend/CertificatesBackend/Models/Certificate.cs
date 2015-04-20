using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace CertificatesBackend.Models
{
	public class Certificate
	{
		public int Id { get; set; }
		public int CertificateSetId { get; set; }
		public int? OrderId { get; set; }

		public string CodeValue { get; set; }
		public virtual CertificateSet CertificateSet { get; set; }
		public virtual Order Order { get; set; } 
	}
}