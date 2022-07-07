const deleteProduct = (productId) => {
    fetch('/delete-product', {
        method: 'POST',
        body: JSON.stringify({ productId: productId }),
    }).then((_res) => {
        window.location.href = '/products'
    });
}

// const updateProduct = (productId) => {
//     fetch('/update_product', {
//         method: 'POST',
//         body: JSON.stringify({ productId: productId }),
//     })
//     // .then((_res) => {
//     //     window.location.href = '/update_product'
//     // });
// }

const addCart = (productId) => {
    fetch('/add-cart', {
        method: 'POST',
        body: JSON.stringify({ productId: productId }),
    }).then((_res) => {
        window.location.href = '/shopping_cart'
    });
}

const deleteCart = (productId) => {
    fetch('/delete-cart', {
        method: 'POST',
        body: JSON.stringify({ productId: productId }),
    }).then((_res) => {
        window.location.href = '/shopping_cart'
    });
}

const product = (productId) => {
    fetch('/product_showcase', {
        method: 'POST',
        body: JSON.stringify({ productId: productId }),
        });
        // .then((_res) => {
        //     window.location.href = '/product_showcase'
        // });
    }

const checkout = (userId) => {
    fetch('/checkout', {
        method: 'POST',
        body: JSON.stringify({ userId: userId }),
    }).then((_res) => {
        window.location.href = '/'
    });
}