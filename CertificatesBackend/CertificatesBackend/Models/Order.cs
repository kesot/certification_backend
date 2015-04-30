using System;

namespace CertificatesBackend.Models
{
	public class Order
	{
		public int Id { get; private set; }

		/// <summary>
		/// Внешний Id пользователя(На бэкэнде юзера не хранятся).
		/// </summary>
		public int UserExternalId { get; set; }

		/// <summary>
		/// Дата создания заказа
		/// </summary>
		public DateTime? CreationDateTime { get; private set; }
		
		/// <summary>
		/// Дата оплаты заказа. Null, пока не оплачен.
		/// </summary>
		public DateTime? PaymentDateTime { get; private set; }

		/// <summary>
		/// Был ли отменен заказ
		/// </summary>
		public bool IsCanceled { get; set; }
	}
}