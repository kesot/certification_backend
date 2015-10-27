using CertificatesBackend.DAL;

namespace CertificatesBackend.Models
{
	public class Company: IEntityWithId
	{
		public int Id { get; set; }
		public string Name { get; set; }
	}
}