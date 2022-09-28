data "aws_iam_role" "test_role" {
  name = "bird-role-p3sj8z1b"

  }


resource "aws_s3_bucket_object" "object" {
  
  bucket = "femi-data-lake"
  key    = "sdg.zip"
  source = "${path.module}/download/sdg.zip"

  etag = filemd5("${path.module}/download/sdg.zip")
}


resource "aws_lambda_function" "test_lambda" {
  depends_on = [aws_s3_bucket_object.object]
  s3_bucket = aws_s3_bucket_object.object.bucket
  s3_key = aws_s3_bucket_object.object.key

  function_name = "generate_thursday_report"
  role          = data.aws_iam_role.test_role.arn
  handler       = "main.handler"
  timeout       = 300
  
  source_code_hash = filebase64sha256("download/sdg.zip")

  runtime = "python3.7"
  layers = ["arn:aws:lambda:${var.aws_region}:336392948345:layer:AWSDataWrangler-Python37:5"]

  environment {
    variables = {
      OUTPUT_BUCKET = "outputbucket"
      INPUT_BUCKET= "inputbucket"
    }
  }
}

resource "aws_cloudwatch_event_rule" "weekly" {
    name = "trigger_lambda_weekly"
    schedule_expression = "cron(0 8 ? * 5 *)"
    
}

resource "aws_cloudwatch_event_target" "call_thursday_preport" {
    rule = aws_cloudwatch_event_rule.weekly.name
    arn = aws_lambda_function.test_lambda.arn
    target_id = aws_lambda_function.test_lambda.function_name
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.function_name
  principal     = "events.amazonaws.com"
  
  
}
