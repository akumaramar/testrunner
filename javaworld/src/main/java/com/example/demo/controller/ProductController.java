package com.example.demo.controller;

import com.example.demo.entity.Product;
import com.example.demo.service.ProductService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Positive;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
@Validated
@Tag(name = "Product", description = "Product management APIs")
public class ProductController {

    private final ProductService productService;

    @GetMapping
    @Operation(summary = "Get all products", description = "Retrieves a list of all products")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved products")
    public ResponseEntity<List<Product>> getAllProducts() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get product by ID", description = "Retrieves a product by its ID")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved the product")
    @ApiResponse(responseCode = "404", description = "Product not found")
    public ResponseEntity<Product> getProductById(@PathVariable @Positive Long id) {
        return ResponseEntity.ok(productService.getProductById(id));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Create a new product", description = "Creates a new product")
    @ApiResponse(responseCode = "201", description = "Product successfully created")
    public ResponseEntity<Product> createProduct(@Valid @RequestBody Product product) {
        return new ResponseEntity<>(productService.createProduct(product), HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Update product", description = "Updates an existing product")
    @ApiResponse(responseCode = "200", description = "Product successfully updated")
    @ApiResponse(responseCode = "404", description = "Product not found")
    public ResponseEntity<Product> updateProduct(
            @PathVariable @Positive Long id,
            @Valid @RequestBody Product product) {
        return ResponseEntity.ok(productService.updateProduct(id, product));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Delete product", description = "Deletes a product")
    @ApiResponse(responseCode = "204", description = "Product successfully deleted")
    @ApiResponse(responseCode = "404", description = "Product not found")
    public ResponseEntity<Void> deleteProduct(@PathVariable @Positive Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/available")
    @Operation(summary = "Get available products", description = "Retrieves all available products")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved available products")
    public ResponseEntity<List<Product>> getAvailableProducts() {
        return ResponseEntity.ok(productService.getAvailableProducts());
    }

    @GetMapping("/search")
    @Operation(summary = "Search products", description = "Search products by name")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved matching products")
    public ResponseEntity<List<Product>> searchProducts(@RequestParam String name) {
        return ResponseEntity.ok(productService.searchProducts(name));
    }

    @GetMapping("/price-less-than")
    @Operation(summary = "Get products by price", description = "Retrieves products with price less than specified value")
    @ApiResponse(responseCode = "200", description = "Successfully retrieved products")
    public ResponseEntity<List<Product>> getProductsByPriceLessThan(
            @RequestParam @Positive Double price) {
        return ResponseEntity.ok(productService.getProductsByPriceLessThan(price));
    }
}
