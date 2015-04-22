using System.Linq;
using System.Web;
using System.Web.Http;
using CertificatesBackend.Areas.HelpPage;
using CertificatesBackend.Models;

namespace CertificatesBackend
{
    public static class WebApiConfig
    {
        public static void Register(HttpConfiguration config)
        {
            // Web API configuration and services

            // Web API routes
            config.MapHttpAttributeRoutes();

				config.Routes.MapHttpRoute(
                name: "DefaultApi",
                routeTemplate: "api/{controller}/{id}",
                defaults: new { id = RouteParameter.Optional }
            );
				config.SetDocumentationProvider(new XmlDocumentationProvider(
					HttpContext.Current.Server.MapPath("App_Data/CertificatesBackend.XML")));

        }
    }
}
