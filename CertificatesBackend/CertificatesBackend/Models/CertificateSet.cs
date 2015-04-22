using System;
using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using CertificatesBackend.DAL;
using Newtonsoft.Json;

namespace CertificatesBackend.Models
{
	public class CertificateSet
	{
		public int Id { get; set; }

		/// <summary>
		/// Строка с номера штрихкода с маской. По ней генерятся конкретные коды сертификатов. Спецсимвол - ?. "3234????3455"
		/// </summary>
		[Required(AllowEmptyStrings = false)]
		public string MaskString { get; set; }

		/// <summary>
		/// Внутреннее название
		/// </summary>
		[Required(AllowEmptyStrings = false)]
		public string AdministrativeName { get; set; }

		/// <summary>
		/// Название для отображения потребителю
		/// </summary>
		[Required(AllowEmptyStrings = false)]
		public string Name { get; set; }

		public string Descitption { get; set; }
		
		[Required]
		public int CompanyId { get; set; }
		
		[JsonIgnore]
		public bool IsInCertificateGeneratingStage { get; private set; }
		
		/// <summary>
		/// Идентификатор того что задача по генерации сертификатов завершена.
		/// </summary>
		public bool AllCertificatesGenerated { get; private set; }

		/// <summary>
		/// Цена для покупателя
		/// </summary>
		[Required]
		public int Price { get; set; }
		
		/// <summary>
		/// Номинал сертификата
		/// </summary>
		[Required]
		public int CostValue { get; set; }
		[JsonIgnore]
		public virtual Company Company { get; set; }

		public void GenerateCertificates(CertificatesDbContext dbContext)
		{
			IsInCertificateGeneratingStage = true;
			dbContext.SaveChanges();
			Task.Run(() =>
			{
				try
				{
					var regex = Regex.Match(MaskString, "\\?+");
					var matchString = regex.Value;
					var length = matchString.Length;
					for (int i = 0; i < Math.Pow(10, length); i++)
					{
						dbContext.Certificates.Add(new Certificate()
						{
							CertificateSetId = Id,
							CodeValue = MaskString.Replace(matchString, i.ToString().PadLeft(length, '0'))
						});
					}
					AllCertificatesGenerated = true;
				}
				finally 
				{
					IsInCertificateGeneratingStage = false;
					dbContext.SaveChanges();
				}
			});
		}
	}
}