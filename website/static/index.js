const deleteNote = (noteId) => {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = '/'
    });
}

const deleteProduct = (productId) => {
    fetch('/delete-product', {
        method: 'POST',
        body: JSON.stringify({ productId: productId }),
    }).then((_res) => {
        window.location.href = '/products'
    });
}


const addCart = (productId) => {
    fetch('/add-cart', {
        method: 'POST',
        body: JSON.stringify({ productId: productId }),
    }).then((_res) => {
        window.location.href = '/shopping_cart'
    });
}