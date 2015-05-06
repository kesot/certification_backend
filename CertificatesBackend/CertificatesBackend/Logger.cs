using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;

namespace CertificatesBackend
{
	public class Logger
	{
		private static Logger instance;
		private static List<string> logQueue;
		private static object locker = new object();
		private static string filePath = HttpContext.Current.Server.MapPath("~/App_Data/Log.txt");
		const int maxQueueCount = 1;

		private Logger()
		{
		}

		public static Logger Instance
		{
			get
			{
				if (instance == null)
				{
					instance = new Logger();
					logQueue = new List<string>();
				}
				return instance;
			}
		}

		public void WriteToLog(string message)
		{
			lock (locker)
			{
				logQueue.Add(message);

				if (logQueue.Count >= maxQueueCount)
				{
					File.AppendAllLines(filePath, logQueue);
				}
			}
		}
	}
}