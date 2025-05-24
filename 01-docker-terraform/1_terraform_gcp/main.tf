terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.36.1"
    }
  }
}

provider "google" {
  # Configuration options
  project = "terraform-dem-460711"
  region  = "australia-southeast1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-dem-460711-terraform-bucket"
  location      = "australia-southeast1"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
