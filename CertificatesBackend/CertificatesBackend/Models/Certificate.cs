using CertificatesBackend.DAL;
using Newtonsoft.Json;

namespace CertificatesBackend.Models
{
	public class Certificate : IEntityWithId
	{
		public int Id { get; set; }
		public int CertificateSetId { get; set; }
		public int? OrderId { get; set; }

		public string CodeValue { get; set; }
		
		public CertificateSet CertificateSet { get; set; }
		[JsonIgnore]
		public virtual Order Order { get; set; }
	}
}