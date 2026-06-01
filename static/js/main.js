// Основной JavaScript файл
console.log('Сайт загружен!');

// Можно добавить всплывающие подсказки Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // Активировать все всплывающие подсказки
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});