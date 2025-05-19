# Ensures proper initialization of models

import app.models.sales
import app.models.user
import app.models.discount
import app.models.product
import app.models.category
import app.models.review
import app.models.order as order
import app.models.support


order.OrderResponse.model_rebuild()
order.OrderProductUpdate.model_rebuild()