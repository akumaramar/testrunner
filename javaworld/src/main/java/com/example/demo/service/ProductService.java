package com.example.demo.service;

import com.example.demo.entity.Product;
import com.example.demo.repository.ProductRepository;
import com.example.demo.exception.ResourceNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class ProductService {

    private final ProductRepository productRepository;

    @Cacheable(value = "products")
    public List<Product> getAllProducts() {
        log.info("Fetching all products");
        return productRepository.findAll();
    }

    @Cacheable(value = "product", key = "#id")
    public Product getProductById(Long id) {
        log.info("Fetching product with id: {}", id);
        return productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Product not found with id: " + id));
    }

    @CacheEvict(value = {"products", "product"}, allEntries = true)
    public Product createProduct(Product product) {
        log.info("Creating new product: {}", product.getName());
        return productRepository.save(product);
    }

    @CacheEvict(value = {"products", "product"}, allEntries = true)
    public Product updateProduct(Long id, Product productDetails) {
        log.info("Updating product with id: {}", id);
        Product product = getProductById(id);
        
        product.setName(productDetails.getName());
        product.setDescription(productDetails.getDescription());
        product.setPrice(productDetails.getPrice());
        product.setQuantity(productDetails.getQuantity());
        product.setAvailable(productDetails.isAvailable());
        
        return productRepository.save(product);
    }

    @CacheEvict(value = {"products", "product"}, allEntries = true)
    public void deleteProduct(Long id) {
        log.info("Deleting product with id: {}", id);
        Product product = getProductById(id);
        productRepository.delete(product);
    }

    @Cacheable(value = "available-products")
    public List<Product> getAvailableProducts() {
        log.info("Fetching available products");
        return productRepository.findAvailableProducts();
    }

    public List<Product> searchProducts(String name) {
        log.info("Searching products with name containing: {}", name);
        return productRepository.findByNameContainingIgnoreCase(name);
    }

    public List<Product> getProductsByPriceLessThan(Double price) {
        log.info("Fetching products with price less than: {}", price);
        return productRepository.findByPriceLessThan(price);
    }
}
