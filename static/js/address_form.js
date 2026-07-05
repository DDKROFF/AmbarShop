// Логика переключения полей формы адреса
document.addEventListener('DOMContentLoaded', function() {
  const checkboxApartment = document.getElementById('id_is_apartment');
  const apartmentFields = document.getElementById('apartmentFields');
  const checkboxApartmentEdit = document.getElementById('id_is_apartment_edit');
  const apartmentFieldsEdit = document.getElementById('apartmentFieldsEdit');

  // Функция для переключения видимости полей квартиры
  function toggleApartmentFields(checkbox, fields) {
    if (checkbox && fields) {
      checkbox.addEventListener('change', function() {
        if (this.checked) {
          fields.style.display = 'block';
        } else {
          fields.style.display = 'none';
        }
      });
    }
  }

  // Переключение для формы добавления
  toggleApartmentFields(checkboxApartment, apartmentFields);

  // Переключение для формы редактирования
  toggleApartmentFields(checkboxApartmentEdit, apartmentFieldsEdit);
});
