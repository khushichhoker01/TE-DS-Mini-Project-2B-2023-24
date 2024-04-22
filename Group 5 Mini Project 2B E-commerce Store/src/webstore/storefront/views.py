from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, Seller, Listing
from market.views import index
from plotly.offline import plot
import plotly.graph_objs as go
from django.db.models import Count  # Import Count



def registerUSeller(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        User.objects.create(
            username= uname,
            password=make_password(pwd),
            email=email,
            phone =  request.POST.get('phone'),
            first_name = request.POST.get('fname'),
            last_name = request.POST.get('lname'),

        )

        user = authenticate(email=email, password=pwd)
        if user:
            login(request, user)
        messages.success(request, 'Registered Successfully')

        return redirect(registerSeller)



    return render(request, 'storefront/register-u-seller.html', context)

@login_required
def registerSeller(request):
    context = {}

    if request.method == 'POST':
        Seller.objects.create(
            user = request.user,
            store_name = request.POST.get('sname'),
            desc = request.POST.get('desc'),

        )
        messages.success(request, 'Registered Successfully')
        return redirect(index)
    
    return render(request, 'storefront/register-seller.html',context)


@login_required
def sellerProfile(request):
    context = {}
    try:
        seller = Seller.objects.get(user=request.user)
        context['seller'] = seller
    except:
        return redirect('index')
    
    return render(request, 'storefront/seller-profile.html', context)




def update_seller_bar():
    # Assuming you have a Seller model with a 'store_name' field
    # Retrieve the actual seller data from the database
    sellers = Seller.objects.all()

    # Extract store names and counts
    store_names = [seller.store_name for seller in sellers]
    seller_counts = [10] * len(sellers)  # You'll need to calculate the actual seller count

    # Create data trace for the bar chart
    data = [
        go.Bar(
            x=store_names,  # x-axis: store names
            y=seller_counts  # y-axis: seller count
        )
    ]

    # Define layout for the bar chart
    layout = go.Layout(title='Seller Count')

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    # Generate HTML for the figure
    seller_bar_html = plot(fig, output_type='div')

    return seller_bar_html


def generate_pie_chart_for_seller(seller_id):
    # Query to get total listings for the seller
    total_listings = Listing.objects.filter(seller=seller_id).count()

    # Query to get count of listings for each category
    category_counts = Listing.objects.filter(seller_id=seller_id).values('product__category__name').annotate(count=Count('id'))

    # Prepare data for the pie chart
    categories = [item['product__category__name'] for item in category_counts]
    counts = [item['count'] for item in category_counts]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=categories, values=counts)])

    # Update layout


    # Show the pie chart
    return fig.to_html(full_html=False, include_plotlyjs=False)

def Dashboard(request, *args, **kwargs):
        users = User.objects.all()
        prod_pie = generate_pie_chart_for_seller(request.user.seller)
        # Update each graph
        seller_bar_html = update_seller_bar()

        # Render the HTML template with the graph HTML content
        return render(request, 'storefront/plotly-graphs.html', {'prod_pie': prod_pie, 'seller_bar_html': seller_bar_html})
    








# Create your views here.
