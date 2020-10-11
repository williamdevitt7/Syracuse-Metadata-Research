# Testing Sub RDA wth tax_id as an attribute (integer) for the assortativity analaysis
# Sarah
# Sept 15 2020

sub96 <- read.csv("E:/GenBank_2020Data/Taxonomy_Network_Analysis/sub_virus/sub_els/sub_virus_el_1996.csv")
df96 <- subset(sub96, select = c("Auth1", "Auth2", "tax_id"))

g <- graph.data.frame(df96, directed=FALSE)  
E(g)$weight <- 1 
#g <- simplify(g, edge.attr.comb="sum")

relations <- data.frame(from=c("Bob", "Cecil", "Cecil", "David",
                               "David", "Esmeralda"),
                        to=c("Alice", "Bob", "Alice", "Alice", "Bob", "Alice"),
                        same.dept=c(FALSE,FALSE,TRUE,FALSE,FALSE,TRUE),
                        friendship=c(4,5,5,2,1,1), advice=c(4,5,5,4,2,3))
# so need to use linked list and then have names and attributes "melted"

r <- reshape(df96, direction='long', 
        varying=c('Auth1', 'Auth2'), 
        v.names=c('Author1', 'Author2'),
        idvar='tax_id')
