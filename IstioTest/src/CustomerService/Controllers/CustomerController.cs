using Microsoft.AspNetCore.Mvc;
using CustomerService.Models;

namespace CustomerService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CustomerController : ControllerBase
    {
        private static readonly List<Customer> _customers = new()
        {
            new Customer
            {
                Id = 1,
                Name = "John Doe",
                Email = "john.doe@example.com",
                Phone = "555-0101",
                Address = "123 Main St, City"
            },
            new Customer
            {
                Id = 2,
                Name = "Jane Smith",
                Email = "jane.smith@example.com",
                Phone = "555-0102",
                Address = "456 Oak Ave, Town"
            },
            new Customer
            {
                Id = 3,
                Name = "Bob Johnson",
                Email = "bob.johnson@example.com",
                Phone = "555-0103",
                Address = "789 Pine Rd, Village"
            }
        };

        [HttpGet]
        public ActionResult<IEnumerable<Customer>> GetAll()
        {
            return Ok(_customers);
        }

        [HttpGet("{id}")]
        public ActionResult<Customer> GetById(int id)
        {
            var customer = _customers.FirstOrDefault(c => c.Id == id);
            if (customer == null)
                return NotFound();

            return Ok(customer);
        }

        [HttpPost]
        public ActionResult<Customer> Create(Customer customer)
        {
            customer.Id = _customers.Max(c => c.Id) + 1;
            _customers.Add(customer);
            return CreatedAtAction(nameof(GetById), new { id = customer.Id }, customer);
        }

        [HttpPut("{id}")]
        public IActionResult Update(int id, Customer customer)
        {
            var existingCustomer = _customers.FirstOrDefault(c => c.Id == id);
            if (existingCustomer == null)
                return NotFound();

            existingCustomer.Name = customer.Name;
            existingCustomer.Email = customer.Email;
            existingCustomer.Phone = customer.Phone;
            existingCustomer.Address = customer.Address;

            return NoContent();
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            var customer = _customers.FirstOrDefault(c => c.Id == id);
            if (customer == null)
                return NotFound();

            _customers.Remove(customer);
            return NoContent();
        }
    }
}
