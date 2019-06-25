$('form').submit(function(e){
    e.preventDefault()
    $.ajax({
      url: /* Where should this go? */,
      method: /* Which HTTP verb? */,
      data: /* Any data to send along? */,
      success: /* What code should we run when the server responds? */
    })
  })