using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Diagnostics;
using System.IO;
using System.Net.Http;
using System.Web.Http.Controllers;
using System.Web.Http.Filters;

namespace CertificatesBackend.Attributes
{
	public class DebugLoggerActionFilterAttribute : ActionFilterAttribute
	{
		public override void OnActionExecuting(HttpActionContext actionContext)
		{
			File.AppendAllText(HttpContext.Current.Server.MapPath("~/App_Data/Log.txt"),
				DateTime.UtcNow.ToString("G") + " " + actionContext.Request + "\r\n");
		}

		public override void OnActionExecuted(HttpActionExecutedContext actionExecutedContext)
		{
			File.AppendAllText(HttpContext.Current.Server.MapPath("~/App_Data/Log.txt"),
			 DateTime.UtcNow.ToString("G") + " " + actionExecutedContext.Response + "\r\n");
		}
	}
}