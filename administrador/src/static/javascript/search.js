function pesquisaAdmin() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaEmpresa() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaCurso() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaEvento() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaJogo() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName('td')[0];
    td
    
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

function pesquisaAluno() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaVideoaula() {
  let input, filter, table, tr, td, i, txtValue;
  
  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaVaga() {
  let input, filter, table, tr, td, i, txtValue;

  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0]; 
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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

function pesquisaCurriculo() {
  let input, filter, table, tr, td, i, txtValue;

  input = document.getElementsByTagName('input')[0];
  filter = input.value.toUpperCase();
  table = document.getElementsByTagName('table')[0];
  tr = table.getElementsByTagName('tr');

  for (i = 0; i < tr.length; i++) {
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