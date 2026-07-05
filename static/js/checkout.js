document.addEventListener('DOMContentLoaded', function() {
  const deliveryMethodSelect = document.getElementById('id_delivery_method');
  const addressSection = document.getElementById('addressSection');
  const hasApartmentCheckbox = document.getElementById('id_has_apartment');
  const apartmentFields = document.getElementById('apartmentFields');
  
  // Переключение формы доставки
  deliveryMethodSelect.addEventListener('change', function() {
    if (this.value === 'courier') {
      addressSection.style.display = 'block';
    } else {
      addressSection.style.display = 'none';
    }
  });
  
  // Переключение полей квартиры
  hasApartmentCheckbox.addEventListener('change', function() {
    if (this.checked) {
      apartmentFields.style.display = 'block';
    } else {
      apartmentFields.style.display = 'none';
    }
  });
  
  // Проверка при загрузке
  if (deliveryMethodSelect.value === 'courier') {
    addressSection.style.display = 'block';
  }
});
