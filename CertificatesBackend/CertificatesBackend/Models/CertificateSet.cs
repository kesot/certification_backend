using System.ComponentModel.DataAnnotations;
using Newtonsoft.Json;

namespace CertificatesBackend.Models
{
	public class CertificateSet
	{
		public int Id { get; set; }
		[Required(AllowEmptyStrings = false)]
		public string MaskString { get; set; }
		[Required(AllowEmptyStrings = false)]
		public string AdministrativeName { get; set; }
		[Required(AllowEmptyStrings = false)]
		public string Name { get; set; }
		public string Descitption { get; set; }
		[Required]
		public int CompanyId { get; set; }
		[JsonIgnore]
		public bool IsInCertificateGeneratingStage { get; set; }
		public bool AllCertificatesGenerated { get; set; }

		// Цена для покупателя
		[Required]
		public int Price { get; set; }
		// Номинал сертификата
		[Required]
		public int CostValue { get; set; }
		[JsonIgnore]
		public virtual Company Company { get; set; }
	}
}