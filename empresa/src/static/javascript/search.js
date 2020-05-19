function pesquisaVaga() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (let i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName('td')[0];
    
    if (td) {
      txtValue = td.textContent || td.innerText;
      
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = '';
      } else {
        tr[i].style.display = 'none';
      }
    }
  }
}

function pesquisaCandidato() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (let i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName('td')[2];
    
    if (td) {
      txtValue = td.textContent || td.innerText;
      
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = '';
      } else {
        tr[i].style.display = 'none';
      }
    }
  }
}