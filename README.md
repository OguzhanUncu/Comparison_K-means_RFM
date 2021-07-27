# K-means clustering vs RFM clustering

## What is our target?

* We want to determine the differences between k-mean clustering and rfm, observing the differences of the clusters.

* Both of them use for clustering and we should know which one is better in a specific situation.
  
## About data

The data in this project is Online Retail which is open source data.

Variables:
* InvoiceNO: Invoice Number, if this code starts with C it means that the operation has been cancelled.
* StockCode: Product Code, unique number for each product.
* Description: Product Name
* Quantity: Product Quantity
* InvoiceDate: Invoice date
* UnitPrice: Invoice price (Sterling)
* CustomerID: Unique customer number
* Country: Country name

### What is k-means and RFM clustering?

#### K-means:
* The algorithm of k-means works iteratively to assign each data point to one of K groups based on the features that are provided.
  Data points are clustered based on feature similarity. Here is an example.
  
 ![img_2](https://user-images.githubusercontent.com/76595310/127180423-715b1114-9431-40ea-a8ec-21acb3f12d49.png)


* The algorithm gets the number of clusters from outside. It can be determined using the elbow method as you can see below.

![myplot](https://user-images.githubusercontent.com/76595310/127175971-cddb47dd-b12d-48d0-8219-8aadf0ded7f9.png)

* The method says the number of clusters should be six.


#### RFM

* Besides the K-means, rfm is a method that needs to be done manually and in this method you have to determine the sets, how the partition points will be.

* You can see our segments according to our data below.

![rfm](https://user-images.githubusercontent.com/76595310/127179109-a520d7e2-dea4-4b06-b892-a734d630db2b.png)

* The green side refers to new customers and 42 customers are in here.

### Comparison

Now we can start making our comparisons.
I would like to evaluate here in two different ways, one with 10 groups and the other as six groups suggested by the elbow method.
The reason I do this is because there are 10 groups in the rfm method. In a way, I wanted to do the same number of groups and see the results.

Below we can see the distribution of k-means groups within the rfm segments.


![mixed](https://user-images.githubusercontent.com/76595310/127188872-99fe50f2-a50c-4d89-957c-8ebc662af11d.png)

I want to share the details of data groupby segments and clusters.

![Numbers](https://user-images.githubusercontent.com/76595310/127192364-574c420e-127b-4319-8502-9c8f9fe5fe59.png)

As you can see, when there are ten groups, the distributions are like this.


* What if we compare by making six groups as the elbow method says? We can see that below.

![seg_1](https://user-images.githubusercontent.com/76595310/127193164-4ca3bb4d-7fad-4a82-8d45-970199a21e31.png)

That's all I have to say for this project, thanks for reading!

