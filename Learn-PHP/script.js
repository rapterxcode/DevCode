// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });
});

// Search Tabs Functionality
document.querySelectorAll('.tab-btn').forEach(button => {
    button.addEventListener('click', function() {
        const tabId = this.dataset.tab;
        
        // Remove active class from all tabs and contents
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        this.classList.add('active');
        document.getElementById(tabId + '-tab').classList.add('active');
    });
});

// Product Category Filter
document.querySelectorAll('.category-btn').forEach(button => {
    button.addEventListener('click', function() {
        const category = this.dataset.category;
        
        // Remove active class from all category buttons
        document.querySelectorAll('.category-btn').forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        
        // Filter products
        document.querySelectorAll('.product-card').forEach(card => {
            if (category === 'all' || card.dataset.category === category) {
                card.style.display = 'block';
                card.style.animation = 'fadeIn 0.5s ease';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

// Numerology Calculator
function calculateNumerology(number) {
    const digits = number.toString().replace(/[^0-9]/g, '');
    let sum = 0;
    
    for (let digit of digits) {
        sum += parseInt(digit);
    }
    
    // Continue reducing until single digit or master number (11, 22, 33)
    while (sum > 9 && sum !== 11 && sum !== 22 && sum !== 33) {
        let tempSum = 0;
        const sumStr = sum.toString();
        for (let digit of sumStr) {
            tempSum += parseInt(digit);
        }
        sum = tempSum;
    }
    
    return sum;
}

// Numerology Meanings
const numerologyMeanings = {
    1: "ความเป็นผู้นำ",
    2: "ความร่วมมือ", 
    3: "ความคิดสร้างสรรค์",
    4: "ความมั่นคง",
    5: "ความเสรี",
    6: "ความรับผิดชอบ",
    7: "ปัญญา",
    8: "ความสำเร็จทางวัตถุ",
    9: "ความเมตตา",
    11: "ความเป็นผู้นำทางจิตวิญญาณ",
    22: "ผู้สร้างฝัน",
    33: "ความรักและการเสียสละ",
    42: "ความสำเร็จในการงาน",
    57: "ความรักและความสัมพันธ์",
    64: "ความมั่งคั่งทางการเงิน"
};

// Search Functionality
document.querySelector('#numerology-tab .btn-search').addEventListener('click', function() {
    const input = document.querySelector('#numerology-tab .search-input');
    const targetSum = parseInt(input.value);
    
    if (!targetSum || targetSum < 1) {
        alert('กรุณาป้อนตัวเลขที่ถูกต้อง');
        return;
    }
    
    // Show loading state
    this.classList.add('loading');
    this.textContent = 'กำลังค้นหา...';
    
    // Simulate search delay
    setTimeout(() => {
        searchByNumerology(targetSum);
        this.classList.remove('loading');
        this.innerHTML = '<i class="fas fa-calculator"></i> คำนวณ';
    }, 1000);
});

function searchByNumerology(targetSum) {
    const products = document.querySelectorAll('.product-card');
    let foundProducts = [];
    
    products.forEach(product => {
        const numberElement = product.querySelector('.product-number');
        const number = numberElement.textContent.replace(/[^0-9]/g, '');
        const calculatedSum = calculateNumerology(number);
        
        if (calculatedSum === targetSum) {
            foundProducts.push(product);
            product.style.display = 'block';
            product.style.border = '3px solid #ffd700';
            product.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            product.style.display = 'none';
            product.style.border = 'none';
        }
    });
    
    if (foundProducts.length === 0) {
        alert(`ไม่พบเบอร์หรือทะเบียนที่มีผลรวม ${targetSum}`);
        // Reset display
        products.forEach(product => {
            product.style.display = 'block';
            product.style.border = 'none';
        });
    } else {
        // Update numerology info
        const meaning = numerologyMeanings[targetSum] || 'ความหมายพิเศษ';
        const infoElement = document.querySelector('.numerology-info');
        infoElement.innerHTML = `
            <p><i class="fas fa-star"></i> พบ ${foundProducts.length} รายการที่มีผลรวม ${targetSum}</p>
            <p><i class="fas fa-info-circle"></i> ความหมาย: ${meaning}</p>
        `;
    }
}

// Order System
document.querySelectorAll('.btn-order').forEach(button => {
    button.addEventListener('click', function() {
        if (this.classList.contains('disabled')) {
            return;
        }
        
        const productCard = this.closest('.product-card');
        const number = productCard.querySelector('.product-number').textContent;
        const price = productCard.querySelector('.product-price').textContent;
        const type = productCard.dataset.category === 'phone' ? 'เบอร์โทรศัพท์' : 'ทะเบียนรถ';
        
        const confirmation = confirm(`ต้องการสั่งซื้อ ${type}: ${number}\nราคา: ${price}\n\nกดตกลงเพื่อดำเนินการต่อ`);
        
        if (confirmation) {
            // Simulate order process
            this.textContent = 'กำลังดำเนินการ...';
            this.classList.add('loading');
            
            setTimeout(() => {
                alert('ขอบคุณสำหรับการสั่งซื้อ!\nเจ้าหน้าที่จะติดต่อกลับภายใน 24 ชั่วโมง');
                
                // Update product status
                const statusBadge = productCard.querySelector('.status-badge');
                statusBadge.textContent = 'จอง';
                statusBadge.className = 'status-badge reserved';
                
                this.textContent = 'จองแล้ว';
                this.classList.add('disabled');
                this.classList.remove('loading');
            }, 2000);
        }
    });
});

// Admin Functions
function showAddForm() {
    document.getElementById('addProductForm').style.display = 'block';
    document.getElementById('addProductForm').scrollIntoView({ behavior: 'smooth' });
}

function hideAddForm() {
    document.getElementById('addProductForm').style.display = 'none';
}

// Admin Form Submission
document.querySelector('#addProductForm form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    // Simulate adding product
    alert('เพิ่มสินค้าเรียบร้อยแล้ว!');
    this.reset();
    hideAddForm();
});

// Contact Form Submission
document.querySelector('.contact-form form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = this.querySelector('input[type="text"]').value;
    const phone = this.querySelector('input[type="tel"]').value;
    const email = this.querySelector('input[type="email"]').value;
    const message = this.querySelector('textarea').value;
    
    if (!name || !phone || !message) {
        alert('กรุณากรอกข้อมูลให้ครบถ้วน');
        return;
    }
    
    // Simulate form submission
    const submitBtn = this.querySelector('.btn-primary');
    submitBtn.textContent = 'กำลังส่ง...';
    submitBtn.classList.add('loading');
    
    setTimeout(() => {
        alert('ส่งข้อความเรียบร้อยแล้ว!\nเจ้าหน้าที่จะติดต่อกลับโดยเร็ว');
        this.reset();
        submitBtn.textContent = 'ส่งข้อความ';
        submitBtn.classList.remove('loading');
    }, 1500);
});

// Phone Number Search
document.querySelector('#number-tab .btn-search').addEventListener('click', function() {
    const network = document.querySelector('#number-tab .filter-select').value;
    const searchQuery = document.querySelector('#number-tab .search-input').value;
    
    if (!searchQuery) {
        alert('กรุณาป้อนเบอร์ที่ต้องการค้นหา');
        return;
    }
    
    searchPhoneNumbers(network, searchQuery);
});

function searchPhoneNumbers(network, query) {
    const products = document.querySelectorAll('.product-card[data-category="phone"]');
    let foundProducts = [];
    
    products.forEach(product => {
        const number = product.querySelector('.product-number').textContent;
        const productNetwork = product.querySelector('.network-badge').textContent.toLowerCase();
        
        const matchesNumber = number.includes(query);
        const matchesNetwork = !network || productNetwork === network;
        
        if (matchesNumber && matchesNetwork) {
            foundProducts.push(product);
            product.style.display = 'block';
            product.style.border = '3px solid #ffd700';
        } else {
            product.style.display = 'none';
            product.style.border = 'none';
        }
    });
    
    if (foundProducts.length === 0) {
        alert('ไม่พบเบอร์ที่ตรงกับเงื่อนไขการค้นหา');
        products.forEach(product => {
            product.style.display = 'block';
            product.style.border = 'none';
        });
    }
}

// License Plate Search
document.querySelector('#license-tab .btn-search').addEventListener('click', function() {
    const province = document.querySelector('#license-tab .filter-select').value;
    const searchQuery = document.querySelector('#license-tab .search-input').value;
    
    if (!searchQuery) {
        alert('กรุณาป้อนทะเบียนที่ต้องการค้นหา');
        return;
    }
    
    searchLicensePlates(province, searchQuery);
});

function searchLicensePlates(province, query) {
    const products = document.querySelectorAll('.product-card[data-category="license"]');
    let foundProducts = [];
    
    products.forEach(product => {
        const number = product.querySelector('.product-number').textContent;
        const productProvince = product.querySelector('.province-badge').textContent;
        
        const matchesNumber = number.includes(query);
        const matchesProvince = !province || productProvince.includes(province);
        
        if (matchesNumber && matchesProvince) {
            foundProducts.push(product);
            product.style.display = 'block';
            product.style.border = '3px solid #ffd700';
        } else {
            product.style.display = 'none';
            product.style.border = 'none';
        }
    });
    
    if (foundProducts.length === 0) {
        alert('ไม่พบทะเบียนที่ตรงกับเงื่อนไขการค้นหา');
        products.forEach(product => {
            product.style.display = 'block';
            product.style.border = 'none';
        });
    }
}

// Smooth Scrolling for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const headerHeight = document.querySelector('.header').offsetHeight;
            const targetPosition = target.offsetTop - headerHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Fade In Animation on Scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, observerOptions);

// Apply fade-in animation to sections
document.querySelectorAll('section').forEach(section => {
    section.classList.add('fade-in');
    observer.observe(section);
});

// Real-time Numerology Calculator for Input Fields
document.addEventListener('input', function(e) {
    if (e.target.classList.contains('search-input') && e.target.closest('#numerology-tab')) {
        const value = e.target.value;
        if (value && !isNaN(value)) {
            const sum = calculateNumerology(value);
            const meaning = numerologyMeanings[sum] || 'ความหมายพิเศษ';
            
            // Show preview
            let preview = document.querySelector('.numerology-preview');
            if (!preview) {
                preview = document.createElement('div');
                preview.className = 'numerology-preview';
                e.target.parentNode.appendChild(preview);
            }
            
            preview.innerHTML = `
                <small style="color: #667eea; margin-top: 5px; display: block;">
                    <i class="fas fa-calculator"></i> ผลรวม: ${sum} - ${meaning}
                </small>
            `;
        }
    }
});

// Add CSS animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);