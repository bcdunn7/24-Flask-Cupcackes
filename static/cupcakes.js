const BASE_URL = "http://localhost:5000";

function generateMarkup(cupcake) {
    return `
    <li>
    ${cupcake.flavor}
    </li>
    `
}

async function getAndShowCupcakes() {
    const resp = await axios.get(`${BASE_URL}/api/cupcakes`);

    for (let cupcake of resp.data.cupcakes) {
        let newCupcake = $(generateMarkup(cupcake));
        $('#cupcakes-list').append(newCupcake);
    };
};


$('#new-cupcake-form').on('submit', async function (evt) {
    evt.preventDefault();

    let flavor = $('#form-flavor').val();
    let size = $('#form-size').val();
    let rating = $('#form-rating').val();
    let image = $('#form-image').val();

    
    const resp = await axios.post("/api/cupcakes", {
        flavor,
        size,
        rating,
        image
    });

    let newCupcake = generateMarkup(resp.data.cupcake)
    $('#cupcakes-list').append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$(getAndShowCupcakes);
