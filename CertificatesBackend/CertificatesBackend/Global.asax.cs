using System.Data.Entity;
using System.Web;
using System.Web.Http;
using System.Web.Mvc;
using CertificatesBackend.DAL;

namespace CertificatesBackend
{
	public class WebApiApplication : HttpApplication
	{
		protected void Application_Start()
		{
			GlobalConfiguration.Configure(WebApiConfig.Register);
			Database.SetInitializer(new CertificateInitializer());
			AreaRegistration.RegisterAllAreas();
		}
	}
}
