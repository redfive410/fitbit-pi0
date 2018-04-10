provider "aws" {
  region     = "${var.aws_region}"
}

resource "aws_iam_role" "lambda-fitbit-role" {
  name = "lambda-fitbit-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "lambda-fitbit-role-policy-document" {
  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:PutParameter"
    ]
    resources = [
      "arn:aws:ssm:*:*:parameter/*"
    ]
  }
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

resource "aws_iam_policy" "lambda-fitbit-role-policy" {
  name = "lambda-fitbit-role-policy"
  path = "/"
  policy = "${data.aws_iam_policy_document.lambda-fitbit-role-policy-document.json}"
}

resource "aws_iam_role_policy_attachment" "policy-attachment" {
  role = "${aws_iam_role.lambda-fitbit-role.name}"
  policy_arn = "${aws_iam_policy.lambda-fitbit-role-policy.arn}"
}

data "archive_file" "fitbit-pi0-get-steps-zip" {
  type        = "zip"
  source_dir = "fitbit-pi0-get-steps/"
  output_path = "fitbit-pi0-get-steps.zip"
}

resource "aws_lambda_function" "lambda-fitbit-pi0-get-steps" {
    filename = "${data.archive_file.fitbit-pi0-get-steps-zip.output_path}"
    function_name = "fitbit-pi0-get-steps"
    role = "${aws_iam_role.lambda-fitbit-role.arn}"
    handler = "lambda_function.lambda_handler"
    runtime = "python3.6"
    timeout = 10
    source_code_hash = "${data.archive_file.fitbit-pi0-get-steps-zip.output_base64sha256}"
}
