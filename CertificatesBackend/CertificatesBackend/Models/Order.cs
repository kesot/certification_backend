using System;
using System.Collections;
using System.Collections.Generic;
using CertificatesBackend.DAL;

namespace CertificatesBackend.Models
{
	public class Order: IEntityWithId
	{
		public Order()
		{
			CreationDateTimeUtc = DateTime.UtcNow;
		}

		public int Id { get; set; }

		/// <summary>
		/// Внешний Id пользователя(На бэкэнде юзера не хранятся).
		/// </summary>
		public int UserExternalId { get; set; }

		/// <summary>
		/// Дата создания заказа
		/// </summary>
		public DateTime? CreationDateTimeUtc { get; private set; }
		
		/// <summary>
		/// Дата оплаты заказа. Null, пока не оплачен.
		/// </summary>
		public DateTime? PaymentDateTimeUtc { get; set; }

		/// <summary>
		/// Был ли отменен заказ
		/// </summary>
		public bool IsCanceled { get; set; }

		/// <summary>
		/// Сертификаты в заказе
		/// </summary>
		public ICollection<Certificate> Certificates { get; set; }
	}
}