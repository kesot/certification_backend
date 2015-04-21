using System;

namespace CertificatesBackend.Models
{
	public class Order
	{
		public int Id { get; set; }
		public int UserExternalId { get; set; }
		public DateTime? CreationDateTime { get; set; }
		public DateTime? PaymentDateTime { get; set; }
	}
}