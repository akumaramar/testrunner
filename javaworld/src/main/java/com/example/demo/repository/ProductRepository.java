package com.example.demo.repository;

import com.example.demo.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    List<Product> findByAvailable(boolean available);
    
    List<Product> findByPriceLessThan(Double price);
    
    @Query("SELECT p FROM Product p WHERE p.quantity > 0 AND p.available = true")
    List<Product> findAvailableProducts();
    
    List<Product> findByNameContainingIgnoreCase(String name);
}
