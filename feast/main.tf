provider "google" {
  project = "mlops-437709"
  region  = "us-central1"
}

# Feature Online Store
resource "google_vertex_ai_feature_online_store" "demo_store" {
  name   = "demo"
  region = "us-central1"

  bigtable {
    auto_scaling {
      min_node_count         = 1
      max_node_count         = 1
      cpu_utilization_target = 70
    }
  }
}

# Template for feature group and features
locals {
  feature_groups = {
    credit_request = [
      "credit_amount", "credit_duration", "installment_commitment", "credit_score"
    ]
    customer_financial_profile = [
      "checking_balance", "savings_balance", "existing_credits", "job_history"
    ]
    credit_context = [
      "purpose", "other_parties", "credit_standing", "assets", "other_payment_plans"
    ]
    customer_demographics = [
      "age", "num_dependents", "residence_since", "sex"
    ]
  }
}


# Feature Groups
resource "google_vertex_ai_feature_group" "feature_groups" {
  for_each    = local.feature_groups
  name        = each.key
  region      = "us-central1"
  description = "Feature group for ${each.key}"

  big_query {
    big_query_source {
      input_uri = "bq://mlops-437709.featurestore_demo.credit_files_with_timestamp"
    }
    entity_id_columns = ["credit_request_id"]
  }
}

# Feature Group Features
resource "google_vertex_ai_feature_group_feature" "credit_request_features" {
  for_each = toset(local.feature_groups.credit_request)

  name          = each.value
  region        = "us-central1"
  feature_group = google_vertex_ai_feature_group.feature_groups["credit_request"].name
  description   = "Feature for ${each.value}"
}

resource "google_vertex_ai_feature_group_feature" "customer_financial_profile_features" {
  for_each = toset(local.feature_groups.customer_financial_profile)

  name          = each.value
  region        = "us-central1"
  feature_group = google_vertex_ai_feature_group.feature_groups["customer_financial_profile"].name
  description   = "Feature for ${each.value}"
}

resource "google_vertex_ai_feature_group_feature" "credit_context_features" {
  for_each = toset(local.feature_groups.credit_context)

  name          = each.value
  region        = "us-central1"
  feature_group = google_vertex_ai_feature_group.feature_groups["credit_context"].name
  description   = "Feature for ${each.value}"
}

resource "google_vertex_ai_feature_group_feature" "customer_demographics_features" {
  for_each = toset(local.feature_groups.customer_demographics)

  name          = each.value
  region        = "us-central1"
  feature_group = google_vertex_ai_feature_group.feature_groups["customer_demographics"].name
  description   = "Feature for ${each.value}"
}


# Feature Online Store FeatureView
resource "google_vertex_ai_feature_online_store_featureview" "main" {
  name                 = "main"
  region               = "us-central1"
  feature_online_store = google_vertex_ai_feature_online_store.demo_store.name
  sync_config {
    cron = "*/10 * * * *"
  }
  feature_registry_source {

    feature_groups { 
        feature_group_id = google_vertex_ai_feature_group.feature_groups["credit_request"].name
        feature_ids      = [google_vertex_ai_feature_group_feature.credit_request_features["credit_amount"].name]
       }
  }
}