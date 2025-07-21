using Microsoft.AspNetCore.Mvc;
using OrderService.Models;

namespace OrderService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class OrderController : ControllerBase
    {
        private static readonly List<Order> _orders = new()
        {
            new Order
            {
                Id = 1,
                CustomerId = 1,
                OrderDate = DateTime.Now.AddDays(-1),
                Status = "Completed",
                TotalAmount = 1099.98M,
                Items = new List<OrderItem>
                {
                    new OrderItem { Id = 1, OrderId = 1, ProductId = 1, ProductName = "Laptop", Quantity = 1, UnitPrice = 999.99M, Subtotal = 999.99M },
                    new OrderItem { Id = 2, OrderId = 1, ProductId = 3, ProductName = "Headphones", Quantity = 1, UnitPrice = 99.99M, Subtotal = 99.99M }
                }
            },
            new Order
            {
                Id = 2,
                CustomerId = 2,
                OrderDate = DateTime.Now,
                Status = "Pending",
                TotalAmount = 599.99M,
                Items = new List<OrderItem>
                {
                    new OrderItem { Id = 3, OrderId = 2, ProductId = 2, ProductName = "Smartphone", Quantity = 1, UnitPrice = 599.99M, Subtotal = 599.99M }
                }
            }
        };

        [HttpGet]
        public ActionResult<IEnumerable<Order>> GetAll()
        {
            return Ok(_orders);
        }

        [HttpGet("{id}")]
        public ActionResult<Order> GetById(int id)
        {
            var order = _orders.FirstOrDefault(o => o.Id == id);
            if (order == null)
                return NotFound();

            return Ok(order);
        }

        [HttpGet("customer/{customerId}")]
        public ActionResult<IEnumerable<Order>> GetByCustomerId(int customerId)
        {
            var customerOrders = _orders.Where(o => o.CustomerId == customerId).ToList();
            return Ok(customerOrders);
        }

        [HttpPost]
        public ActionResult<Order> Create(Order order)
        {
            order.Id = _orders.Max(o => o.Id) + 1;
            order.OrderDate = DateTime.Now;
            
            foreach (var item in order.Items)
            {
                item.Id = (_orders.Any() ? _orders.SelectMany(o => o.Items).Max(i => i.Id) : 0) + 1;
                item.OrderId = order.Id;
            }
            
            _orders.Add(order);
            return CreatedAtAction(nameof(GetById), new { id = order.Id }, order);
        }

        [HttpPut("{id}/status")]
        public IActionResult UpdateStatus(int id, [FromBody] string status)
        {
            var order = _orders.FirstOrDefault(o => o.Id == id);
            if (order == null)
                return NotFound();

            order.Status = status;
            return NoContent();
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            var order = _orders.FirstOrDefault(o => o.Id == id);
            if (order == null)
                return NotFound();

            _orders.Remove(order);
            return NoContent();
        }
    }
}
