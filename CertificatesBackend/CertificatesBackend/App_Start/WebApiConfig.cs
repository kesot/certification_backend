using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
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
			config.MessageHandlers.Add(new LogRequestAndResponseHandler());

		}
	}
	public class LogRequestAndResponseHandler : DelegatingHandler
	{
		protected override async Task<HttpResponseMessage> SendAsync(
			  HttpRequestMessage request, CancellationToken cancellationToken)
		{
			//logging request body
			string requestString = request.ToString();
			string requestBody = await request.Content.ReadAsStringAsync();
			Trace.WriteLine(requestBody);
			string path = HttpContext.Current.Server.MapPath("~/App_Data/Log1.txt");
			File.AppendAllText(path, "Request: " +
				DateTime.UtcNow.ToString("G") + " " + requestString + "\r\n" + "Reauest body: " + requestBody + "\r\n");

			//let other handlers process the request
			return await base.SendAsync(request, cancellationToken)
				 .ContinueWith(task =>
				 {
					 //once response is ready, log it
					 var responseBody = task.Result.Content.ReadAsStringAsync().Result;
					 File.AppendAllText(path, "Respnse: " + 
						DateTime.UtcNow.ToString("G") + " " + responseBody + "\r\n");

					 return task.Result;
				 });
		}
	}
}
